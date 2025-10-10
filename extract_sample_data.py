#!/usr/bin/env python3.11
"""
Extract sample data from MAWN QC SQL dump for portfolio projects
Focus on a few stations with complete data for modeling
"""

import gzip
import re
import pandas as pd
from datetime import datetime
import sys

def extract_hourly_data_from_sql(sql_gz_path, output_csv, max_records=50000):
    """
    Extract hourly data from SQL dump and save to CSV
    Parse INSERT statements for hourly tables
    """
    
    print(f"Extracting data from {sql_gz_path}...")
    
    # Track which station we're currently processing
    current_table = None
    station_data = []
    total_records = 0
    
    # We'll focus on a few stations for the portfolio
    target_stations = ['aetna', 'albion', 'allegan', 'alpine', 'bath']
    
    with gzip.open(sql_gz_path, 'rt', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if line_num % 100000 == 0:
                print(f"Processed {line_num} lines, collected {total_records} records...")
            
            # Detect table context
            if 'COPY public.' in line and '_hourly' in line:
                # Extract station name
                match = re.search(r'COPY public\.(\w+)_hourly', line)
                if match:
                    station_name = match.group(1)
                    if station_name in target_stations:
                        current_table = station_name
                        print(f"\nFound hourly table for station: {station_name}")
                    else:
                        current_table = None
                continue
            
            # Check for end of COPY block
            if line.strip() == '\\.' or line.strip().startswith('--'):
                if current_table:
                    print(f"Finished reading {current_table}_hourly")
                current_table = None
                continue
            
            # Parse data lines when we're in a target table
            if current_table and line.strip() and not line.startswith('--'):
                try:
                    # Split by tabs (PostgreSQL COPY format)
                    fields = line.strip().split('\t')
                    
                    if len(fields) >= 29:  # Ensure we have enough fields
                        # Parse the key fields based on the hourly table structure
                        record = {
                            'station': current_table,
                            'year': int(fields[0]) if fields[0] != '\\N' else None,
                            'day': int(fields[1]) if fields[1] != '\\N' else None,
                            'hour': int(fields[2]) if fields[2] != '\\N' else None,
                            'rpt_time': int(fields[3]) if fields[3] != '\\N' else None,
                            'date': fields[4] if fields[4] != '\\N' else None,
                            'time': fields[5] if fields[5] != '\\N' else None,
                            'atmp': float(fields[6]) if fields[6] not in ['\\N', ''] else None,
                            'atmp_src': fields[7] if fields[7] != '\\N' else None,
                            'relh': float(fields[8]) if fields[8] not in ['\\N', ''] else None,
                            'relh_src': fields[9] if fields[9] != '\\N' else None,
                            'dwpt': float(fields[10]) if fields[10] not in ['\\N', ''] else None,
                            'dwpt_src': fields[11] if fields[11] != '\\N' else None,
                            'pcpn': float(fields[12]) if fields[12] not in ['\\N', ''] else None,
                            'pcpn_src': fields[13] if fields[13] != '\\N' else None,
                            'lws0_pwet': float(fields[14]) if fields[14] not in ['\\N', ''] else None,
                            'lws0_pwet_src': fields[15] if fields[15] != '\\N' else None,
                            'wspd': float(fields[18]) if len(fields) > 18 and fields[18] not in ['\\N', ''] else None,
                            'wspd_src': fields[19] if len(fields) > 19 and fields[19] != '\\N' else None,
                            'wdir': float(fields[20]) if len(fields) > 20 and fields[20] not in ['\\N', ''] else None,
                            'srad': float(fields[24]) if len(fields) > 24 and fields[24] not in ['\\N', ''] else None,
                            'srad_src': fields[25] if len(fields) > 25 and fields[25] != '\\N' else None,
                            'stmp_05cm': float(fields[26]) if len(fields) > 26 and fields[26] not in ['\\N', ''] else None,
                            'stmp_10cm': float(fields[28]) if len(fields) > 28 and fields[28] not in ['\\N', ''] else None,
                            'smst_05cm': float(fields[34]) if len(fields) > 34 and fields[34] not in ['\\N', ''] else None,
                            'smst_10cm': float(fields[36]) if len(fields) > 36 and fields[36] not in ['\\N', ''] else None,
                            'rpet': float(fields[46]) if len(fields) > 46 and fields[46] not in ['\\N', ''] else None,
                        }
                        
                        station_data.append(record)
                        total_records += 1
                        
                        if total_records >= max_records:
                            print(f"\nReached maximum records ({max_records}), stopping extraction...")
                            break
                            
                except (ValueError, IndexError) as e:
                    # Skip malformed lines
                    continue
            
            if total_records >= max_records:
                break
    
    # Convert to DataFrame
    print(f"\nConverting {len(station_data)} records to DataFrame...")
    df = pd.DataFrame(station_data)
    
    # Create datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    
    # Sort by station and datetime
    df = df.sort_values(['station', 'datetime'])
    
    # Save to CSV
    print(f"Saving to {output_csv}...")
    df.to_csv(output_csv, index=False)
    
    print(f"\nExtraction complete!")
    print(f"Total records: {len(df)}")
    print(f"Stations: {df['station'].unique()}")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"\nData summary:")
    print(df.describe())
    
    return df

if __name__ == '__main__':
    sql_gz_path = '/home/ubuntu/upload/mawndb_qc-20250827.sql.gz'
    output_csv = '/home/ubuntu/enviroweather_projects/mawn_hourly_sample.csv'
    
    df = extract_hourly_data_from_sql(sql_gz_path, output_csv, max_records=100000)

