# orchestrator.py
import logging
import azure.functions as func
import azure.durable_functions as df
from lib.tools import say_something

def orchestrator_function(context: df.DurableOrchestrationContext):
    # Wait for an external event named "MyEvent"
    say_something("Waiting for external event 'MyEvent'")
    event_data = yield context.wait_for_external_event("MyEvent")
    say_something(f"Received event: {event_data}")
    if not context.is_replaying: 
        logging.info(f"Received event: {event_data}")

    tasks = []
    # For each enterprise, create parallel tasks for greeting managers and employees.
    for enterprise in event_data.get('enterprises', []):
        enterprise_name = enterprise.get('name')
        sub_tasks = []
        # Greet each manager and in turn, each employee under that manager.
        for manager in enterprise.get('members', []):
            # Director greeting the manager.
            manager_greeting = f"Hello {manager['user']} from director at {enterprise_name}"
            sub_tasks.append(context.call_activity('hello_activity', manager_greeting))
            # Director greeting each employee of the manager.
            for employee in manager.get('members', []):
                employee_greeting = f"Hello {employee['user']} from director at {enterprise_name}"
                sub_tasks.append(context.call_activity('hello_activity', employee_greeting))
        
        # Run all greetings for the current enterprise in parallel.
        tasks.append(context.task_all(sub_tasks))
    
    # Wait for all enterprises' greetings to complete concurrently.
    all_results = yield context.task_all(tasks)
    say_something("Orchestration completed")
    
    return {
        "EventData": event_data,
        "ActivityResults": all_results
    }

main = df.Orchestrator.create(orchestrator_function)