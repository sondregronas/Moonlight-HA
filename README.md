# Moonlight-HA [<img align="right" src=media/coffee.png>](https://www.buymeacoffee.com/JSz8KGIkD)<br>
A custom Home Assistant component for getting the status of an Nvidia Gamestream PC. Currently only displays whether or not a stream is active. I'm going to look into being able to add more details like where the stream is coming from, what is being streamed, or whatever data I can find. You don't have to use Moonlight, as it uses data from the host running the Nvidia Gamestream.<br><br>

To use simply download the 'moonlight' folder and move it to the custom_components folder in your Moonlight config (Create one if it's not there) and add the following to your configuration.yaml:

```
moonlight:
  host: <ip/address_of_host>
  name: Moonlight (default)
  icon: 'mdi:cast' (default)
  icon_active: 'mdi:cast-connected' (default)
```
