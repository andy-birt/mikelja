########## This section I added to run this file in debug in VS Code ##########
import sys
import os
# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
###############################################################################

from scrapers import Linkedin

test = Linkedin(params={ "keywords": "python", "location": "United States" })

r = test.get_results()

print(r)