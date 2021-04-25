import tqdm
from Handlers.WebscrapingHandler import WebscrapingHandler

try:
    handler = []
    handler += [WebscrapingHandler()]

    callables = ['read_input_data', 'process_input_data', 'write_output_data']
    for com in handler:
        for call in tqdm.tqdm(callables, desc="Processing {}".format(type(com).__name__), leave=False):
            getattr(com, call)()
            print()
except Exception as e:
    print(e)