# Data Format

This algorithm expects structured tabular data with four feature columns and one target column.

Feature Columns:
- Irradiation from sensor 1 in watts per square meter (W/m²)
- Irradiation from sensor 2 in watts per square meter (W/m²)
- Ambient temperature in degrees celsius (°C)
- Module temperature in degrees celsius (°C)

Target Column:
- Power produced by the solar panels in kilowatts (kW)

Here is an example:

| from        | to          | W/m²   | W/m²   | kW    | °C     | °C     |
|-------------|-------------|--------|--------|-------|--------|--------|
| 3/5/19 0:00 | 3/5/19 1:00 | 53.075 | 52.466 | 6.495 | 13.009 | 12.050 |
| 3/5/19 1:00 | 3/5/19 2:00 | 10.946 | 10.409 | 0.008 | 11.807 | 8.498  |
| 3/5/19 2:00 | 3/5/19 3:00 | 0.000  | 0.000  | 0.000 | 10.325 | 5.683  |

The date-time columns are not used in the model itself; they are used for dataset filtering and plotting.
