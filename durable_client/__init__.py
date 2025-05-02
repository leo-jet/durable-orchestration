# durable_client.py
import logging
import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    # Change the name from 'orchestrator_function' to 'orchestrator'
    instance_id = await client.start_new('orchestrator', None, None)

    logging.info(f"Started orchestration with ID = {instance_id}")

    return client.create_check_status_response(req, instance_id)