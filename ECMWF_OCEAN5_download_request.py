#!/usr/bin/env python
# install Climate Data Store (CDS) Application Program Interface (API)
# pip install cdsapi
import os
import cdsapi
import asyncio

async def download_multi_level_data():
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-oras5',
        {
            'format': 'tgz',
            'variable': [
                'potential_temperature', 'rotated_meridional_velocity', 'rotated_zonal_velocity',
                'salinity',
            ],
            'vertical_resolution': 'all_levels',
            'year': '2022',
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'product_type': 'operational',
        },
        'multi_lev.tar.gz'
    )

async def download_single_level_data():
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-oras5',
        {
            'format': 'tgz',
            'variable': 'sea_surface_height',
            'vertical_resolution': 'single_level',
            'year': '2022',
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'product_type': 'operational',
        },
        'single_lev.tar.gz'
    )

# Run the asynchronous functions
loop = asyncio.get_event_loop()
loop.run_until_complete(download_multi_level_data())
loop.run_until_complete(download_single_level_data())

# Add os.rename and welcoming message after the downloads
os.rename('multi_lev.tar.gz', 'multi_lev_final.tar.gz')
os.rename('single_lev.tar.gz', 'single_lev_final.tar.gz')
print("Downloads completed! Welcome to the CROCO community.")

