from langchain_core.callbacks import BaseCallbackHandler
import time
class LatencyHandler(BaseCallbackHandler):
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        super().__init__()
        
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        
        self.start_time = time.time() / 1000 / 60
        print(f"Start Time:{self.start_time}")
        
    def on_llm_end(self, response, *, run_id, parent_run_id = None, **kwargs):
        self.end_time = time.time() / 1000 / 60
        print(f"End Time:{self.end_time}")
        
        
        latency = self.end_time - self.start_time
        print(f"Time Spent:{ latency }")