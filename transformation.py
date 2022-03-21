import psycopg2
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


filter_query = '''
    CREATE OR REPLACE MATERIALIZED VIEW filter_data AS
    SELECT *
    FROM clean_data_view
    WHERE %s != %s;
    '''
z_std_query = '''
    CREATE OR REPLACE MATERIALIZED VIEW normalized_data AS(
    WITH stats as
        (SELECT avg(%s) as mean,
            stddev(%s) as sd
        FROM clean_data_view)
    SELECT
        corr_id,
        key_1,
        abs(%s - stats.mean) / stats.sd as z_score_%s
    FROM stats,
        clean_data_view);
    ''' % (config.normalize_column, config.normalize_column, config.normalize_column, config.normalize_column)

math_query = '''
CREATE OR REPLACE MATERIALIZED VIEW math_data AS
SELECT
corr_id,
key_1,
pow(cont_10,3) + exp(cont_9) as math_transform_11
FROM clean_data_view;
'''

# Query to have data available only when all transformation events are complete, otherwise they are left out
transform_query = '''
    CREATE OR REPLACE MATERIALIZED VIEW transformed_data AS
    SELECT filter_data.corr_id,
    filter_data.key_1,
    date_2,
    cont_3,
    cont_4,
    disc_5,
    disc_6,
    cat_7,
    cat_8,
    cont_9,
    cont_10,
    math_data.math_transform_11,
    z_score_%s
    FROM filter_data 
    INNER JOIN normalized_data ON filter_data.corr_id = normalized_data.corr_id
    INNER JOIN math_data ON normalized_data.corr_id = math_data.corr_id
    ''' % config.normalize_column


def main():
    conn = psycopg2.connect(port=6875, dbname="materialize", user="materialize")
    # Materialized view can't be built with transaction so we set isolation level accordingly
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(filter_query, (config.filter_column, config.filter_column_value))
    cur.execute(z_std_query)
    cur.execute(math_query)
    cur.execute(transform_query)


if __name__ == '__main__':
    main()
