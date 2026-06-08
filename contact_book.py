import json
import os

FILENAME = "contacts.json"


# ─── File Handling ────────────────────────────────────────────────────────────

def load_contacts():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts):
    with open(FILENAME, "w") as f:
        json.dump(contacts, f, indent=2)


# ─── Display ──────────────────────────────────────────────────────────────────

def show_contacts(contacts):
    if not contacts:
        print("\n  No contacts found! Add some first.")
        return
    print("\n  YOUR CONTACTS")
    print("  " + "=" * 55)
    print(f"  {'#':<4} {'Name':<20} {'Phone':<15} {'Category'}")
    print("  " + "-" * 55)
    for i, c in enumerate(contacts, 1):
        print(f"  {i:<4} {c['name']:<20} {c['phone']:<15} {c['category']}")
    print("  " + "=" * 55)
    print(f"  Total: {len(contacts)} contacts\n")


def show_contact_detail(contact):
    print("\n  " + "-" * 30)
    print(f"  Name     : {contact['name']}")
    print(f"  Phone    : {contact['phone']}")
    print(f"  Email    : {contact['email'] or 'N/A'}")
    print(f"  Category : {contact['category']}")
    print("  " + "-" * 30)


# ─── Core Functions ───────────────────────────────────────────────────────────

def add_contact():
    print("\n  ADD CONTACT")
    print("  " + "-" * 20)

    name = input("  Name: ").strip()
    if not name:
        print("  Name cannot be empty!")
        return

    phone = input("  Phone: ").strip()
    if not phone:
        print("  Phone cannot be empty!")
        return

    email = input("  Email (optional): ").strip()

    print("  Category: 1.Family  2.Friend  3.Work  4.Other")
    cat_choice = input("  Choose (1-4): ").strip()
    categories = {"1": "Family", "2": "Friend", "3": "Work", "4": "Other"}
    category = categories.get(cat_choice, "Other")

    contacts = load_contacts()
    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "category": category
    })
    contacts.sort(key=lambda c: c["name"].lower())
    save_contacts(contacts)
    print(f"\n  Contact '{name}' added successfully!")


def search_contact():
    contacts = load_contacts()
    query = input("\n  Search (name/phone/email): ").strip().lower()
    if not query:
        return

    results = [
        c for c in contacts
        if query in c["name"].lower()
        or query in c["phone"]
        or query in c["email"].lower()
    ]

    if not results:
        print(f"  No contacts found for '{query}'")
    else:
        print(f"\n  Found {len(results)} result(s):")
        for c in results:
            show_contact_detail(c)


def update_contact():
    contacts = load_contacts()
    show_contacts(contacts)
    if not contacts:
        return

    try:
        num = int(input("  Enter contact number to update: "))
        if not (1 <= num <= len(contacts)):
            print("  Invalid number!")
            return
    except ValueError:
        print("  Please enter a valid number!")
        return

    contact = contacts[num - 1]
    print(f"\n  Updating: {contact['name']}")
    print("  (Press Enter to keep current value)\n")

    name = input(f"  Name [{contact['name']}]: ").strip()
    phone = input(f"  Phone [{contact['phone']}]: ").strip()
    email = input(f"  Email [{contact['email']}]: ").strip()

    if name:
        contact["name"] = name
    if phone:
        contact["phone"] = phone
    if email:
        contact["email"] = email

    contacts.sort(key=lambda c: c["name"].lower())
    save_contacts(contacts)
    print("\n  Contact updated successfully!")


def delete_contact():
    contacts = load_contacts()
    show_contacts(contacts)
    if not contacts:
        return

    try:
        num = int(input("  Enter contact number to delete: "))
        if not (1 <= num <= len(contacts)):
            print("  Invalid number!")
            return
    except ValueError:
        print("  Please enter a valid number!")
        return

    contact = contacts[num - 1]
    confirm = input(f"  Delete '{contact['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        contacts.pop(num - 1)
        save_contacts(contacts)
        print(f"  Contact '{contact['name']}' deleted!")
    else:
        print("  Cancelled.")


def show_by_category():
    contacts = load_contacts()
    if not contacts:
        print("\n  No contacts found! Add some first.")
        return

    categories = ["Family", "Friend", "Work", "Other"]
    for cat in categories:
        group = [c for c in contacts if c["category"] == cat]
        if group:
            print(f"\n  {cat.upper()} ({len(group)})")
            print("  " + "-" * 30)
            for c in group:
                print(f"  {c['name']} — {c['phone']}")


# ─── Menu ─────────────────────────────────────────────────────────────────────

def show_menu():
    print("\n  CONTACT BOOK")
    print("  " + "=" * 25)
    print("  1. View all contacts")
    print("  2. Add contact")
    print("  3. Search contact")
    print("  4. Update contact")
    print("  5. Delete contact")
    print("  6. View by category")
    print("  7. Exit")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("\n  Welcome to your Contact Book!")

    while True:
        show_menu()
        choice = input("\n  Choose an option (1-7): ").strip()

        if choice == "1":
            show_contacts(load_contacts())
        elif choice == "2":
            add_contact()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            show_by_category()
        elif choice == "7":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
