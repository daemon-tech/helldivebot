'''@bot.tree.command(name="planetinfo", description="Fetch Information of a Planet!")
async def planetinfo(interaction: discord.Interaction):
    #data_status = fetch_data_from_api("/api/801/status")
    data_planet = fetch_data_from_api("/api/801/planets")
    if data_planet:
        embed = discord.Embed(title=":ringed_planet: Planet Intel :ringed_planet:", color=discord.Color.blue())
        for i in range(len(data_planet)):
            data_planet_status = fetch_data_from_api(f"/api/801/planets/{i}/status")
            print(int(data_planet_status['liberation']))
            if data_planet_status['liberation'] < 100 and data_planet_status['liberation'] > 0:
                embed.add_field(name="Planet:", value=f"{data_planet_status['planet']['name']}", inline=True)
                embed.add_field(name="ID:", value=f"{i}", inline=True)
                embed.add_field(name="", value=" ", inline=False)
        await interaction.response.send_message(embed=embed)
    else:        
        await interaction.response.send_message("Failed to fetch data from the API. Code 429 : Too many requests!")
        
        #api/801/planets/(index)/status
'''

'''
for i in range(0, len(fetch_data_from_api("/api/801/info")['home_worlds'])):
                for j in range(0, len(fetch_data_from_api("/api/801/info")['home_worlds'][i]['planets'])):
                    embed.add_field(name="Homeworld", value=fetch_data_from_api("/api/801/info")['home_worlds'][i]['planets'][j]['name'], inline=True)
                    embed.add_field(name="Race", value=fetch_data_from_api("/api/801/info")['home_worlds'][i]['race'], inline=True)
'''
