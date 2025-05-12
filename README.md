# TTCStreetcarDelay
Data source: https://open.toronto.ca/dataset/ttc-streetcar-delay-data/

### Understanding the source data

**Streetcar**

|Field Name| Description                                                      |Example|
|---|------------------------------------------------------------------|---|
|_id| Unique identifier for the record                                 |1|
|Date| Date (YYYY/MM/DD)                                                |2025-01-01|
|Line| TTC subway line                                                  |504 KING|
|Time| Time (24h clock)                                                 |02:10|
|Day| Name of the day of the week                                      |Wednesday|
|Station| TTC subway station name                                          |KING AND PARLIAMENT|
|Code| TTC delay code                                                   |MTSAN|
|Min Delay| Delay (in minutes) to the schedule for the following bus         |10|
|Min Gap| Time length (in minutes) from the bus ahead of the following bus |20|
|Bound| Direction of the bus route |W|
|Vehicle| Vehicle number                                                   |4569|

**Delay Code**

| Field Name  | Description                        | Example |
|-------------|------------------------------------|---------|
| _id         | Unique identifier for the code     | 6       |
| CODE        | Delay code                         | ETCE    |
| DESCRIPTION | Humanized description for the code | COMMUNICATION EQUIPMENT (INCLUDES STOP ANNOUNCEMENT)    | 
