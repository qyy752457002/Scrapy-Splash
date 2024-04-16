-- 这个脚本是一个用于Scrapy Splash的Lua脚本，用于在爬取页面时控制Splash的行为。
-- 在这个脚本中，我们可以通过添加自定义的HTTP头部和cookie来模拟登录。

function main(splash, args)
    -- Change User-Agent (Option 1)
    -- splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")

    -- Change User-Agent (Option 2)
    -- headers = {
    --     ['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    -- }

    -- splash:set_custom_headers(headers)
    
    -- Change User-Agent (Option 3)
    splash: on_request(function(request)
        request: set_header('User-Agent',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')

        -- 添加任何其他的自定义headers和cookies
        -- request:set_header('Authorization', 'Bearer YourTokenHere')
        -- request:set_cookie("cookie_name", "cookie_value")
    end)

    -- If a website doesn't render correctly, disabling Private mode might help
    splash.private_mode_enabled = false
    -- Go to the URL set on the splash browser and then wait 3 seconds to let the page render
    assert(splash:go(args.url))
    assert(splash:wait(3))
    -- Select all the elements that have the css selector "label.btn.btn-sm.btn-primary"
    all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
    -- Two elements were selected. We want to click on the second button, then wait 3 seconds to let the page render
    all_matches[2]: mouse_click()
    assert (splash:wait(3))
    -- Increase the viewport to make all the content visible
    splash: set_viewport_full()
    return {splash: png(), splash: html()}
end

-- 每个请求中都设置了一个自定义的User-Agent头部，并添加了一个Bearer token作为Authorization头部，以及一个自定义的cookie。
-- 可以根据需要添加更多的头部和cookie。
-- 通过这种方式，你可以在爬取过程中模拟登录行为，以便访问需要身份验证的页面或资源。