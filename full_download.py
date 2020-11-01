import sys
from th_asset_export import asset_export
from th_vuln_export import vuln_export

if __name__ == '__main__':
    days = sys.argv[1]
    asset_export(days)
    vuln_export(days)

