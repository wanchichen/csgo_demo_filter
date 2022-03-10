# csgo_demo_filter
 
A quick python script that will filter out the demos where you got highlight reel worthy moments in.

## Instructions
1. Export your demos to XLSX format via [CSGO Demo Manager](https://github.com/akiver/CSGO-Demos-Manager). Choose to export as multiple files.
2. Put the script in the same directory as the exported XLSX files.
3. ```
   python filter.py --players <names of players you want to track> --stats <the stats that you want to filter by>, --demo_folder <the location of your replays>, --copy_demos <if you want to copy the filtered out demos to a new directory>
   ```

## Example

```
python filter.py --players shox kennyS --stats 4K 5K "1v3 won" --demo_folder "D:\\replays" --copy_demos True
```
