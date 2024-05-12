def create_thread(client):
    thread = client.beta.threads.create()
    thread_id = thread.id
    return thread_id


def create_message(client, thread_id, text):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text,
    )
    return message.id


def create_run_messages(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id, poll_interval_ms=2000)

    print(run.status)
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        message_content = messages.data[0].content[0].text

        # Remove annotations
        annotations = message_content.annotations
        for annotation in annotations:
            message_content.value = message_content.value.replace(annotation.text, '')

        response_message = message_content.value
        response_message = response_message.strip("`")
        response_message = response_message.strip("json")
        response_message = response_message.strip()
        # Remove the word json and backticks
        print(response_message)
        return response_message
