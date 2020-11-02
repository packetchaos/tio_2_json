import time
import json
from api_wrapper import request_data

time.ctime()
current_time = time.strftime('%b_%d_%Y')


def vuln_export(days):
    start = time.time()
    # Set URLS for threading
    urls = []

    # Set the payload to the maximum number of assets to be pulled at once
    day = 86400
    new_limit = day * int(days)
    day_limit = time.time() - new_limit
    pay_load = {"num_assets": 500, "filters": {"last_found": int(day_limit), "state": ["fixed", "open", "reopened"],
                                               "severity": ["critical", "high", "medium", "low"]}}
    try:
        # request an export of the data
        export = request_data('POST', '/vulns/export', payload=pay_load)

        # grab the export UUID
        ex_uuid = export['export_uuid']
        print('\nRequesting Vulnerability Export with ID : {}'.format(ex_uuid))

        # set a variable to True for our While loop
        not_ready = True

        # now check the status
        status = request_data('GET', '/vulns/export/' + ex_uuid + '/status')

        # status = get_data('/vulns/export/89ac18d9-d6bc-4cef-9615-2d138f1ff6d2/status')
        print("Status : {}".format(str(status["status"])))

        # loop to check status until finished
        while not_ready is True:
            # Pull the status, then pause 5 seconds and ask again.
            if status['status'] == 'PROCESSING' or 'QUEUED':
                time.sleep(2.5)
                status = request_data('GET', '/vulns/export/' + ex_uuid + '/status')
                # print("Status : " + str(status["status"]))

            # Exit Loop once confirmed finished
            if status['status'] == 'FINISHED':
                ptime = time.time()
                print("\nProcessing Time took : {}".format(str(ptime - start)))

                # Display how many chunks there are
                avail = status['total_chunks']
                print("\nChunks Available - {}".format(avail))
                print("Downloading chunks now...hold tight...This can take some time\n")
                not_ready = False

            # Tell the user an error occured
            if status['status'] == 'ERROR':
                print("Error occurred")

        # grab all of the chunks and craft the URLS for threading
        for y in status['chunks_available']:
            chunk_data = request_data('GET', '/vulns/export/{}/chunks/{}'.format(ex_uuid, str(y)))

            with open('vuln_data_{}_chunk_{}.json'.format(current_time, y), 'a') as json_file:
                json.dump(chunk_data, json_file)
                json_file.close()

        end = time.time()
        print("Vulnerability Update Time took : {}\n".format(str(end - start)))

    except KeyError:
        print("Well this is a bummer; you don't have permissions to download Asset data :( ")

    except TypeError:
        print("You may not be authorized or your keys are invalid")



