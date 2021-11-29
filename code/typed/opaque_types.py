from typing import NewType

# order_id = 123
# company_id = 3

# def find_company_order(company_id: int, order_id: int) -> str:
#     return f"company_id={company_id} order_id={order_id}"

# print(find_company_order(order_id, company_id))

OrderId = NewType('OrderId', int)
CompanyId = NewType('Companyid', int)

order_id = OrderId(123)
company_id = CompanyId(3)
def find_company_order(company_id: CompanyId, order_id: OrderId) -> str:
    return f"company_id={company_id} order_id={order_id}"

find_company_order(order_id, company_id)
