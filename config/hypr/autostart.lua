-- Extra autostart processes.
-- o.launch_on_start("my-service")

-- Ask for the SSH key passphrase once per login (Omarchy gcr SSH agent; nothing stored on disk).
o.launch_on_start("/home/kyle/.local/bin/ssh-unlock")
