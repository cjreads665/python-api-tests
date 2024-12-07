import requests
import uuid

ENDPOINT = "https://todo.pixegami.io"


def test_can_get_endpoint():
    response = requests.get(ENDPOINT)
    response.status_code == 200
    pass

def update_task(payload):
    return requests.put(ENDPOINT+"/update-task",json=payload)

def list_tasks(user_id):
    return requests.get(ENDPOINT+'/list-tasks/'+user_id)

def test_can_create_task():
    payload = new_task_payload()
    
    # print(response_create_task.json())
    #extracting the task id from task property insiude the response object
    response_create_task = create_task(payload)
    task_id = response_create_task.json()["task"]["task_id"]
    # print(task_id)

    response_get_task = get_task(task_id)
    get_task_data = response_get_task.json()

    '''
    assert that the content and user_id sent as payload match
    '''
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = new_task_payload()
    task_id = create_task(payload).json()["task"]["task_id"]
    new_payload = {
        "content" : "update test",
        "user_id" : payload["user_id"],
        "task_id" : task_id,
        "is_done" : True
    }

    update_task_response = update_task(new_payload)
    print(update_task_response.json())
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    assert get_task_response.json()["task_id"] == new_payload["task_id"]

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    #List tasks
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    assert len(list_task_response.json()["tasks"]) == 3

# helper functions
def create_task(payload):
    # print(ENDPOINT+'/create-task')
    response_create_task = requests.put(ENDPOINT+'/create-task', json=payload)
    assert response_create_task.status_code == 200
    return response_create_task

def get_task(task_id):
    response_get_task = requests.get(ENDPOINT+f"/get-task/{task_id}")
    assert response_get_task.status_code == 200
    return response_get_task



def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_user_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }