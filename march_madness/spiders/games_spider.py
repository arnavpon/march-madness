import scrapy
import json

# Goal - AI search algorithm down tree
# search farthest depth by seed
# search farthest depth by team

class GamesSpider(scrapy.Spider):
    name = "games"
    is_start = True  # indicates whether crawling first page or links

    start_urls = [
        "https://www.ncaa.com/basketball-men/d1/every-ncaa-bracket-1939-today-tournament-stats-records"
    ]

    def parse(self, response):
        if self.is_start:
            # crawling home page, get outbound links
            self.is_start = False  # update indicator
            self.log("\n\n\n----- Crawling Home Page... ------")
            #tournament_links = response.css('article.bro-hr a::attr(href)').getall()
            # self.log(f' Found {len(tournament_links)} outbound links')
            # self.log(tournament_links[0:2])
            # for page in tournament_links:
            #     yield response.follow(page, callback=self.parse)

            # follow all links manually...
            for year in range(1939, 2020):
                # get all data - URL structure varies erratically so we need to do multiple requests to get data for all the tournaments
                for d in range(1, 32):
                    self.log(f"\n\nYear {year}")
                    day = d if d > 9 else f"0{d}"
                    yield response.follow(f"https://www.ncaa.com/news/basketball-men/article/2020-05-{day}/{year}-ncaa-tournament-bracket-scores-stats-records", callback=self.parse)
                    yield response.follow(
                        f"https://www.ncaa.com/news/basketball-men/article/2020-05-{day}/{year}-ncaa-tournament-bracket-scores-stats-rounds",
                        callback=self.parse)
                    yield response.follow(
                        f"https://www.ncaa.com/news/basketball-men/article/2020-05-{day}/{year}-ncaa-tournament-brackets-scores-stats-records",
                        callback=self.parse)

        else:
            # crawling tournament pages
            self.log(f"\n Crawling url {response.url}")
            year = response.url.split("/")[7][0:4]  # get tournament year from url
            self.log(f"Tournament year: {year}")
            filepath = f"march_madness/data/bracket_{year}.jl"

            # Extract game data
            scores_table = response.css('h2 + ul > li')  # gets scores data list items
            titles = scores_table.css("li > em").xpath("text()").getall()
            game_data = dict()
            for i, block in enumerate(scores_table):
                games = block.css('ul > li').getall()
                if i < len(titles):
                   game_data[titles[i]] = games
                else:  # some pages have unitalicized Final Four games
                    game_data["Final Four"] = games

            with open(filepath, 'w') as f:
                f.write(json.dumps(game_data))
            self.log('parsed page!')