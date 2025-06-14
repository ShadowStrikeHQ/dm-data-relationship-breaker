# dm-data-relationship-breaker
Identifies and breaks relationships between data points to prevent re-identification. For example, it could randomly reassign addresses to individuals within a city to eliminate direct linkages. - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## Install
`git clone https://github.com/ShadowStrikeHQ/dm-data-relationship-breaker`

## Usage
`./dm-data-relationship-breaker [params]`

## Parameters
- `-h`: Show help message and exit
- `--city`: The city to reassign addresses within.
- `--num_records`: The number of records to generate and reassign.
- `--output_file`: No description provided
- `--seed`: Optional seed for Faker

## License
Copyright (c) ShadowStrikeHQ
