import asyncio
from playwright.async_api import async_playwright
import datetime
import time



async def click_login(email, password, target_hour=10, target_min=27):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Run in headful mode to watch the automation
        page = await browser.new_page()

        await page.goto('https://resy.com/cities/new-york-ny/venues/da-claudio-ny?date=2024-07-29&seats=2')

        login_selector = 'text="Log in"'  
        await page.wait_for_selector(login_selector, state="visible")
        await page.click(login_selector)

        login_selector = 'text="Use Email and Password instead"'  
        await page.wait_for_selector(login_selector, state="visible")
        await page.click(login_selector)


        await page.fill('input[name="email"]', email)
        await page.fill('input[name="password"]', password)


        login_selector = 'text="Continue"'  
        await page.wait_for_selector(login_selector, state="visible")
        await page.click(login_selector)

        try:
            login_selector = 'text="No Thanks"'  
            await page.wait_for_selector(login_selector, state="visible")
            await page.click(login_selector)
        except:
            print("No Continue Button")

        while True:
            now = datetime.datetime.now()
            if now.hour == target_hour and now.minute == target_min:
                break
            # Sleep for a short while to prevent a tight loop that consumes high CPU
            await asyncio.sleep(10)  # Check every 10 second


        # It's 9:00 AM, refresh the page
        await page.reload()
        print("Page refreshed at exactly 9:00 AM.")


        try:
            login_selector = 'text="No Thanks"'  
            await page.wait_for_selector(login_selector, state="visible")
            await page.click(login_selector)
        except:
            print("No Continue Button")

        # select date and time of reservation button

        counter = 0
        while counter < 2:  
            await page.wait_for_selector('button:has-text("PM")', timeout=5000)  # Wait up to 5 seconds for any PM button to appear
            
            buttons = await page.query_selector_all('button:has-text("PM")')
            if buttons:
                print("Clicked the first available button.")
                await buttons[0].click()  # Clicks the first button that contains "PM"
                
                try:
                    await page.screenshot(path='before_click.png')
                    await page.evaluate("() => { document.querySelector('text=\"Reserve Now\"').click(); }")
                    await page.screenshot(path='after_click.png')
                    print("JS")
                except:
                    # Now, wait and click the RESERVE NOW button
                    #await page.wait_for_load_state('networkidle')  # Ensures network activity has settled down
                    # Directly click the button, assuming it's loaded
                    await page.click('button > span:text("Reserve Now")')
                    await page.screenshot(path='error_screenshot.png')

                

                break
            else:
                print("No available buttons found, refreshing.")
                await page.reload()  # Refresh the page if no buttons are found
            counter += 1

        await page.wait_for_timeout(50000)

        print("DONE")

        await browser.close()

asyncio.run(click_login("zoardarma@gmail.com", "ILoveAryBoo!1"))

#Z*RKR9M3tg.rm_x

"""
counter = 0
        while counter < 2:  
            await page.wait_for_selector('button:has-text("PM")', timeout=5000)  # Wait up to 5 seconds for any PM button to appear
            
            buttons = await page.query_selector_all('button:has-text("PM")')
            if buttons:
                print("Clicked the first available button.")
                await buttons[0].click()  # Clicks the first button that contains "PM"
                
                # Now, wait and click the RESERVE NOW button
                reserve_button_selector = 'text="RESERVE NOW"'
                await page.wait_for_selector(reserve_button_selector, state="visible")
                await page.click(reserve_button_selector)
                
                break
            else:
                print("No available buttons found, refreshing.")
                await page.reload()  # Refresh the page if no buttons are found
            counter += 1
"""