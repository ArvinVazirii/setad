from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from setad.spiders.manghul import get_manghul

configure_logging()
setting = get_project_settings()
runner = CrawlerRunner(setting)

runner.crawl(get_manghul)

run = runner.join()
run.addBoth(lambda _: reactor.stop())

reactor.run()
