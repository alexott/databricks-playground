from databricks.sdk import WorkspaceClient

workspace_client = WorkspaceClient()


for se in workspace_client.serving_endpoints.list():
    # print(f"Analyzing {se.name}")
    should_do_check = False
    if se.config.served_entities:
        for entity in se.config.served_entities:
            if entity.external_model or entity.foundation_model or entity.entity_name.startswith("system.ai."):
                should_do_check = True
                break
            
    if not should_do_check:
        continue
    found_problems = []
    # print(f"Checking {se.name}")
    if not se.ai_gateway:
        found_problems.append("No AI Gateway found")
    else:
        if not se.ai_gateway.guardrails:
            found_problems.append("No guardrails found")
        else:
            if not se.ai_gateway.guardrails.input:
                found_problems.append("No input guardrails found")
            if not se.ai_gateway.guardrails.output:
                found_problems.append("No output guardrails found")
        
        if not se.ai_gateway.inference_table_config or not se.ai_gateway.inference_table_config.enabled:
            found_problems.append("Inference table is not enabled") 
                
    if found_problems:
        print(f"Found problems for {se.name}: {found_problems}")
    # else:
    #     print(f"No problems found for {se.name}")
    





