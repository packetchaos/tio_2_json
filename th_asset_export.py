import time
import json
from api_wrapper import request_data

time.ctime()
current_time = time.strftime('%b_%d_%Y')


def asset_export(days):
    start = time.time()

    # Set the payload to the maximum number of assets to be pulled at once
    day = 86400
    new_limit = day * int(days)
    day_limit = time.time() - new_limit
    pay_load = {"chunk_size": 500, "filters": {"last_assessed": int(day_limit)}}
    try:
        # request an export of the data
        export = request_data('POST', '/assets/export', payload=pay_load)

        # grab the export UUID
        ex_uuid = export['export_uuid']
        print('\nRequesting Asset Export with ID : {}'.format(ex_uuid))

        # set a variable to True for our While loop
        not_ready = True

        # now check the status
        status = request_data('GET', '/assets/export/' + ex_uuid + '/status')

        print("Status : {}".format(str(status["status"])))

        # loop to check status until finished
        while not_ready is True:
            # Pull the status, then pause 2.5 seconds and ask again.
            if status['status'] == 'PROCESSING' or 'QUEUED':
                time.sleep(2.5)
                status = request_data('GET', '/assets/export/' + ex_uuid + '/status')
                # print("Status : " + str(status["status"]))

            # Exit Loop once confirmed finished
            if status['status'] == 'FINISHED':
                ptime = time.time()
                print("\nProcessing Time took : {}".format(str(ptime - start)))
                not_ready = False

            # Tell the user an error occured
            if status['status'] == 'ERROR':
                print("Error occurred")

        # grab all of the chunks and craft the URLS for threading
        for y in status['chunks_available']:
            chunk_data = request_data('GET', '/assets/export/{}/chunks/{}'.format(ex_uuid, str(y)))

            with open('asset_data_{}_chunk_{}.json'.format(current_time, y), 'w') as json_file:
                json.dump(chunk_data, json_file)
                json_file.close()

        end = time.time()
        print("Asset Download took: {}\n".format(str(end - start)))

    except IndexError:
        print("Well this is a bummer; you don't have permissions to download Asset data :( ")
    except TypeError:
        print("You may not be authorized or your keys are invalid")
