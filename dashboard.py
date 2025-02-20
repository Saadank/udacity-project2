import psycopg2
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_query(query, conn):
    """Executes a query and returns a Pandas DataFrame"""
    df = pd.read_sql(query, conn)
    return df

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    

    queries = {
        "Most Played Songs": """
        SELECT songs.title, COUNT(*) AS play_count
        FROM songplays
        JOIN songs ON songplays.song_id = songs.song_id
        GROUP BY songs.title
        ORDER BY play_count DESC
        LIMIT 10;
        """,
        "User Activity by Level": """
        SELECT level, COUNT(*) AS user_count
        FROM users
        GROUP BY level;
        """,
        "Peak Listening Time": """
        SELECT time.hour, COUNT(*) AS plays
        FROM songplays
        JOIN time ON songplays.start_time = time.start_time
        GROUP BY time.hour
        ORDER BY plays DESC;
        """
    }
    
    for title, query in queries.items():
        df = run_query(query, conn)
        print(f"\n{title}:")
        print(df)
        
        # Plot if the query has meaningful data
        if "play_count" in df.columns:
            plt.figure(figsize=(10,5))
            sns.barplot(x=df['title'], y=df['play_count'], palette="viridis")
            plt.xticks(rotation=90)
            plt.title(title)
            plt.xlabel("Song Title")
            plt.ylabel("Play Count")
            plt.show()
        elif "plays" in df.columns:
            plt.figure(figsize=(10,5))
            sns.barplot(x=df['hour'], y=df['plays'], palette="viridis")
            plt.title(title)
            plt.xlabel("Hour of the Day")
            plt.ylabel("Number of Plays")
            plt.show()

    conn.close()

if __name__ == "__main__":
    main()