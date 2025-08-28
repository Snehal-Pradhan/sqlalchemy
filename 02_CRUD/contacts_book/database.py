from sqlalchemy.orm import sessionmaker
from models import engine,Contact
Session = sessionmaker(bind=engine)

class ContactNotFoundError(Exception):
    pass

def add_contact(name, phone, email, category):
    session = Session()
    new_contact = Contact(name = name,phone=phone,email=email,category=category)
    session.add(new_contact)
    session.commit()
    session.close()

def get_all_contacts():
    session = Session()
    contact_list = session.query(Contact).all()
    session.close()
    return contact_list

def get_contacts_by_category(category):
    session = Session()
    category_contact = session.query(Contact).filter(Contact.category == category).all()
    session.close()
    return category_contact

def update_contact(contact_id, new_name, new_phone, new_email, new_category): 
    session = Session()
    selected_user = session.query(Contact).filter(Contact.id == contact_id).first()
    if selected_user is None:
        raise ContactNotFoundError(f"Contact with ID {contact_id} not found.")
    
    selected_user.name = new_name
    selected_user.phone = new_phone
    selected_user.email = new_email
    selected_user.category = new_category
    session.commit()
    session.close()

def delete_contact(contact_id):
    session = Session()
    selected_user = session.query(Contact).filter(Contact.id == contact_id).first()
    if selected_user is None:
        raise ContactNotFoundError(f"Contact with ID {contact_id} not found.")
    
    session.delete(selected_user)
    session.commit()
    session.close()

