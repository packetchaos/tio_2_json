import sys
from th_asset_export import asset_export
from th_vuln_export import vuln_export

if __name__ == '__main__':
    days = sys.argv[1]
    # the second argument '0' is to tell the code to request a new export ID.  Alternatively, you could use an external ID.
    # the third argument '1' is to tell the code to use a single thread.  Keep this value to 1 unless writing to a DB
    asset_export(days, '0', 1)
    vuln_export(days, '0', 1)
