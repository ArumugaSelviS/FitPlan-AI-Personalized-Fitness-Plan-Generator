import os
import time

os.environ["GEMINI_API_KEY"] = "**************************************"

!pkill -f streamlit

!streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false &>/content/logs.txt &

time.sleep(3)

from google.colab import output
output.serve_kernel_port_as_window(8501)
