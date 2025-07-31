
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ussd import handle_ussd


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ussd")
async def ussd(request: Request):
    form_data = await request.form()
    return handle_ussd(form_data)
