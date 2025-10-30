from petstore.pet_store_schema_client.client import Client
from petstore.pet_store_schema_client.api.pet import get_pet_by_id

# クライアントを初期化
client = Client(base_url="http://localhost:8080")

# pet_id=1 のペットを取得
pet = get_pet_by_id.sync(pet_id=1, client=client)

print(f"Pet: {pet}")
