from tools import tools, ThreadExecutionStatus


class Helper:
    def __init__(self, client):
        self.client = client

    def include_message_and_process_response(self, question, thread, assistant, model) -> str:
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=question
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            tools=tools,
            model=model
        )

        ran = self.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        while ran.status != ThreadExecutionStatus.COMPLETED.value:
            print('Gerando caso: ', ran.status)
            ran = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if ran.status == ThreadExecutionStatus.FAILED.value:
                raise Exception('Erro na OpenAI: ' + ran['last_error'])

        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )

        return messages.data[0].content[0].text.value
