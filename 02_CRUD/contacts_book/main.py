from database import get_all_contacts,get_contacts_by_category,delete_contact,update_contact,add_contact

def main():
    while True:
        print("\n--- Contacts Book ---")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. View by Category")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("Q. Quit")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            category = input("Category: ")
            add_contact(name, phone, email, category)

        elif choice == '2':
            contacts = get_all_contacts()
            for contact in contacts:
                print(f"{contact.id}: {contact.name} - {contact.phone} - {contact.email} ({contact.category})")
        
        elif choice == "3":
            category = input("Category: ")
            contacts = get_contacts_by_category(category=category)
            for contact in contacts:
                print(f"{contact.id}: {contact.name} - {contact.phone} - {contact.email} ({contact.category})")
        elif choice == "4":
            id = input("Enter ID :")
            name = input("Enter new name:")
            phone = input("Enter new phone:")
            email = input("Enter new email:")
            category = input("Enter new category:")
            update_contact(id,new_name=name,new_phone=phone,new_email=email,new_category=category)
        elif choice == "5":
            id = input("Enter ID :")
            delete_contact(id)
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()