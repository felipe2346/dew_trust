# from decimal import Decimal, InvalidOperation
# from django.utils import timezone
# from transaction.models import Transaction  # Update to your actual model import

# CHARGE_FIELDS = [
#     'beneficiary_name', 'beneficiary_account', 'beneficiary_bank',
#     'iban_number', 'description', 'route_code', 'transaction_type',
#     'transaction_date', 'transaction_time', 'beneficiary_address', 'bank_address'
# ]

# def create_charge_transaction_from(transaction, charges=Decimal('65.00')):
#     """
#     Creates a charge transaction based on an existing transaction.

#     Args:
#         transaction (Transaction): The original transaction instance.
#         charges (Decimal or str or float): The charge amount. Defaults to 65.00.

#     Returns:
#         Transaction: The newly created charge transaction.
#     """
#     if not isinstance(transaction, Transaction):
#         raise ValueError("Expected a Transaction instance")
    
#     try:
#         charge_amount = Decimal(charges)
#     except (InvalidOperation, TypeError):
#         raise ValueError("Charges must be a valid number or Decimal")

#     charge_data = {field: getattr(transaction, field) for field in CHARGE_FIELDS}
#     charge_data['amount'] = charge_amount
#     charge_data['description'] = f"Charge for for wire transafer with transaction ID {transaction.id}"
#     charge_data['transaction_date'] = timezone.now().date()
#     charge_data['transaction_time'] = timezone.now().time()

#     return Transaction.objects.create(**charge_data)



# from decimal import Decimal
# from transactions.utils import create_charge_transaction_from

# # Use default charge
# create_charge_transaction_from(transaction)

# # Custom charge amount
# create_charge_transaction_from(transaction, charges=Decimal('99.99'))

# # Or from float/string (will still be safely converted)
# create_charge_transaction_from(transaction, charges=75.5)
# create_charge_transaction_from(transaction, charges='100.00')

from decimal import Decimal, InvalidOperation
from django.utils import timezone
from transaction.models import Transaction  # Adjust as per your project structure

def create_charge_transaction_from(transaction, charges=Decimal('65.00')):
    """
    Creates a charge transaction based on an existing transaction.

    Args:
        transaction (Transaction): The original transaction instance.
        charges (Decimal or str or float): The charge amount. Defaults to 65.00.

    Returns:
        Transaction: The newly created charge transaction.
    """
    if not isinstance(transaction, Transaction):
        raise ValueError("Expected a Transaction instance")

    try:
        charge_amount = Decimal(charges)
    except (InvalidOperation, TypeError):
        raise ValueError("Charges must be a valid number or Decimal")
    
    account = transaction.account 

    # Ensure there's enough balance to deduct the charge
    if account.balance < charge_amount:
        raise ValueError("Insufficient balance to deduct the charge.")
    
    # Deduct the charge from main balance
    account.balance -= charge_amount
    account.save()  # Save the updated balance

    now = timezone.now()

    # Ensure all required fields are populated
    charge_data = {
        'account': transaction.account,
        'beneficiary_name': "DewTrust",
        'beneficiary_account': "****DewTrust",
        'beneficiary_bank': "DewTrust",
        'iban_number': transaction.iban_number,
        'description': f"Charge for wire transfer with transaction ID {transaction.id}",
        'route_code': transaction.route_code or 'DDXTRY4563',
        'transaction_type': 'DR',
        'status': 'Successful',  
        'transaction_date': now.date(),
        'transaction_time': now.time(),
        'beneficiary_address': transaction.beneficiary_address,
        'bank_address': transaction.bank_address,
        'amount': charge_amount,
        'balance_after_transaction': transaction.balance_after_transaction - charge_amount,
    }

    return Transaction.objects.create(**charge_data)
