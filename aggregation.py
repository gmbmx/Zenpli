import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

group_query = '''
    CREATE OR REPLACE MATERIALIZED VIEW grouped_data AS
    SELECT sum(cont_10) as sum_cont_10,
        date_2
    FROM transformed_data
    GROUP BY date_2
    ORDER BY date_2;
    '''
aggregation_query = '''
    CREATE OR REPLACE MATERIALIZED VIEW unique_data AS
    SELECT count(distinct cat_7) as cat_7_unique_values
    FROM transformed_data;
    '''


def main():
    conn = psycopg2.connect(port=6875, dbname="materialize", user="materialize")
    # Materialized view can't be built with transaction so we set isolation level accordingly
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(group_query)
    cur.execute(aggregation_query)


if __name__ == '__main__':
    main()
