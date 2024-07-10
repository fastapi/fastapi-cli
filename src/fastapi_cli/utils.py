def generate_markdown(api_spec, title):
    md = []

    # Info
    info = api_spec.get("info", {})
    if title:
        words = [word.capitalize() for word in title.split(" ")]
        title = " ".join(words)
        md.append(f"# {title}")
    else:
        md.append(f"# {info.get('title', 'API Documentation')}")
    md.append(f"\n## Version: {info.get('version', 'N/A')}\n")

    # Paths
    md.append("### Paths\n")
    paths = api_spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            md.append(f"#### {path}\n")
            md.append(f"**{method.upper()}**\n")
            md.append(f"**Summary:** {details.get('summary', 'No summary')}\n")
            md.append(f"**Operation ID:** {details.get('operationId', 'N/A')}\n")

            # Parameters
            parameters = details.get("parameters", [])
            if parameters:
                md.append("**Parameters:**\n")
                md.append("| Name | In | Required | Schema | Description | Example |")
                md.append("|------|----|----------|--------|-------------|---------|")
                for param in parameters:
                    name = param.get("name", "N/A")
                    param_in = param.get("in", "N/A")
                    required = param.get("required", False)
                    schema = param.get("schema", {})
                    schema_str = f"`type: {schema.get('type', 'N/A')}`<br>`title: {schema.get('title', 'N/A')}`"
                    if "description" in schema:
                        schema_str += f"<br>`description: {schema.get('description', 'N/A')}`"
                    if "enum" in schema:
                        schema_str += f"<br>`enum: {schema.get('enum')}`"
                    if "default" in schema:
                        schema_str += f"<br>`default: {schema.get('default')}`"
                    description = param.get("description", "N/A")
                    example = param.get("example", "N/A")
                    md.append(
                        f"| {name} | {param_in} | {required} | {schema_str} | {description} | {example} |"
                    )

            # Request Body
            request_body = details.get("requestBody", {})
            if request_body:
                md.append("**Request Body:**")
                md.append(f"- **Required:** {request_body.get('required', False)}")
                md.append(f"- **Content:**")
                content = request_body.get("content", {})
                for content_type, content_schema in content.items():
                    md.append(f"  - **{content_type}:**")
                    schema_ref = content_schema.get("schema", {}).get("$ref", "N/A")
                    md.append(
                        f"    - **Schema:** [{schema_ref.split('/')[-1]}](#{schema_ref.split('/')[-1].lower()})\n"
                    )

            # Responses
            responses = details.get("responses", {})
            if responses:
                md.append("**Responses:**\n")
                md.append("| Status Code | Description | Content |")
                md.append("|-------------|-------------|---------|")
                for status, response in responses.items():
                    description = response.get("description", "N/A")
                    content = response.get("content", {})
                    content_str = ""
                    for content_type, content_schema in content.items():
                        schema_ref = content_schema.get("schema", {}).get("$ref", "N/A")
                        content_str += f"{content_type}: `schema: [{schema_ref.split('/')[-1]}](#{schema_ref.split('/')[-1].lower()})`<br>"
                    md.append(f"| {status} | {description} | {content_str.strip('<br>')} |")

    # Components
    components = api_spec.get("components", {}).get("schemas", {})
    if components:
        md.append("### Components")
        md.append("#### Schemas")
        for schema_name, schema_details in components.items():
            md.append(f"##### {schema_name}")
            md.append(f"- **Type:** {schema_details.get('type', 'N/A')}")
            if "required" in schema_details:
                md.append(f"- **Required:** {', '.join(schema_details.get('required', []))}")
            md.append(f"- **Title:** {schema_details.get('title', 'N/A')}")
            md.append("- **Properties:**")
            properties = schema_details.get("properties", {})
            for prop_name, prop_details in properties.items():
                prop_type = prop_details.get("type", "N/A")
                prop_format = prop_details.get("format", "N/A")
                prop_title = prop_details.get("title", "N/A")
                prop_desc = prop_details.get("description", "N/A")
                md.append(f"  - **{prop_name}:**")
                md.append(f"    - **Type:** {prop_type}")
                if prop_format != "N/A":
                    md.append(f"    - **Format:** {prop_format}")
                md.append(f"    - **Title:** {prop_title}")
                md.append(f"    - **Description:** {prop_desc}")

    return "\n".join(md)
