## A tool to create hypixel skyblock texture packs from png files

this converts png files into a useable hypixel skyblock texture pack

run `main.js`, select the input and output directories when prompted and it will map all the textures to their respective models as listed in `id_models.json`.

the pack name will be the same as the input directory.
also gets pack.png from there.

any unassigned textures will be output to the logs folder in the repo for you to look through.

if there's an issue such as a missing id for an item, open an issue on github so it can be fixed.

its a bit fragile atm so make sure you have a pack.png and clean input folder to be safe.

## configs and animated textures
#### if you only care about basic static textures then theres no need to read this.

you can add animated textures by placing the png and mcmeta file in a folder named the same as the id.

you can add configs as well.

add a config.json file in a folder the same way.

```json
{
    ["model"]: "custom_model_name",
    ["held"]: "custom_model_name"
}
```

model will set the custom model for the texture, held requires 2 textures for held and gui.

held searches for a 'item_id.png' and 'item_id_held.png' file in the folder and will be used for the gui texture and use the normal generated model, and held will show as the held item with the specified custom model.

held overrides model config, aka model will do nothing while held is used.