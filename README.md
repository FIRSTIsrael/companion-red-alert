# companion-red-alert
A small python docker to alert the Companion when there is a red alert during an event.

## Configuring Companion
In Companion, configure a button that will be pressed when a red alert is triggered for the configured zones. Make sure your Companion server is running on the localhost interface.

## Building the Docker
`docker build -t red-alert-companion .`

## Running the Docker

### Setting envionment variables
`COMPANION_HOSTNAME`: Companion server url including port, e.g. `http://localhost:8000`
`COMPANION_BUTTON_LOCATION`: Page row and column, separated by commas, e.g. 1,3,7
`RED_ALERT_ZONES`: Zone names to track, in Hebrew, separated by columns, e.g. "תל אביב - מרכז,תל אביב - עבר הירקון"
`TEST_MODE`: Set this to True to send a test notification when the program starts.


`docker run -d -it --name red-alert-companion --env COMPANION_HOSTNAME=<hostname> --env COMPANION_BUTTON_LOCATION=<page,row,column> --env RED_ALERT_ZONES=<zone1,zone2,zone3> --restart=always --add-host host.docker.internal:host-gateway red-alert-companion`

Note: Make sure the Hebrew place names are not reversed!