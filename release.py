import random
import string
from playwright.sync_api import sync_playwright
import time

choice = input("Enter 1 To Generate Usernames, Passwords and Emails\nEnter 2 to Upvote Posts on Reddit\n--> ")

if choice == '1':
    def generate_random_string(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def get_temp_email():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, channel='msedge')
            context = browser.new_context()
            page = context.new_page()
            
            page.goto("https://www.tempmailaddress.com/")
            
            # Wait for the email address to load
            page.wait_for_selector("#email")
            
            # Get the email address
            email_address = page.query_selector("#email").inner_text()
            
            # Close the browser
            browser.close()
            
            return email_address

    # Ask the user for the number of sets
    num_sets = int(input("Enter the number of sets you want: "))

    # Generate the specified number of sets and store them in a list
    sets = []
    for _ in range(num_sets):
        username = generate_random_string()
        password = generate_random_string()
        email = get_temp_email()
        sets.append((username, password, email))

    # Store the sets in a text file
    with open("UPE.txt", "w") as file:
        for i, (username, password, email) in enumerate(sets, start=1):
            file.write(f"Set {i}:\n")
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n")
            file.write(f"Email: {email}\n")
            file.write("\n")

    print(f"{num_sets} sets of username, password, and email have been stored in UPE.txt.")

elif choice == '2':
    with open("Logins.txt") as file:
        credentials = [line.strip().split(":") for line in file.readlines()]

    with open("Posts.txt") as file:
        posts = [line.strip().split(" ", 1) for line in file.readlines()]

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, channel='msedge')

        for post in posts:
            upvotes = int(post[0])
            post_url = post[1]

            random.shuffle(credentials)  # Shuffle the list of credentials

            for i in range(upvotes):
                username, password = random.choice(credentials)  # Select a random credential

                context = browser.new_context()

                try:
                    page = context.new_page()

                    # Navigate to Reddit and log in
                    page.goto("https://www.reddit.com/login")
                    time.sleep(1)
                    page.fill('input[name="username"]', username)
                    page.fill('input[name="password"]', password)
                    page.click('button[type="submit"]')

                    # Wait for login to complete and navigate to the post URL
                    time.sleep(3)
                    page.goto(post_url)

                    print(f'Upvoting Post {post_url}\n')
                    page.click(".icon-upvote")
                    print(f'Post Upvoted with Username: {username}\n')

                except Exception as e:
                    print(f"An error occurred: {str(e)}")

                finally:
                    # Close the page and clear cookies
                    page.close()
                    context.clear_cookies()

                # Pause for a few seconds before moving to the next upvote
                time.sleep(1)

            # Close the context after all upvotes for the current post
            context.close()

        # Close the browser after all posts and upvotes are processed
        browser.close()
