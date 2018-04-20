# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from time import sleep
import random

count = 2

def generateYear(info, index):
    ordinals = ['st', 'nd', 'rd']
    monthName = {
        'January' : '1',
        'February' : '2',
        'March' : '3',
        'April' : '4',
        'May' : '5',
        'June' : '6',
        'July' : '7',
        'August' : '8',
        'September' : '9',
        'October' : '10',
        'November' : '11',
        'December' : '12'
    }
    year = info[index[0]-1]
    day = info[index[0]-2]
    for s in ordinals:
        day = day.replace(s, '')
    if(not day.isdigit()):
        day = '1'
    if (info[index[0]-3] in monthName):
        month = monthName[info[index[0]-3]]
    else:
        month = monthName['December']

    formattedDate = year + '-' + month + '-' + day

    return formattedDate



class Book19Spider(Spider):
    name = 'book19'
    allowed_domains = ["goodreads.com"]
    start_urls = ["http://goodreads.com/list/show/16/"]

    def parse(self, response):
        books = response.xpath('//tr/td[3]')

        for book in books:
            page_url = book.xpath('.//*[@class="bookTitle"]/@href').extract_first()
            abs_page_url = response.urljoin(page_url)

            yield Request(url = abs_page_url, callback = self.parse_page)

        sleep(random.randrange(2,3))
        global count
        count -= 1

        next_page = response.xpath('//*[@class="pagination"]/a[@class="next_page"]/@href')
        if(count > 0 and next_page):
            next_page_url = next_page.extract_first()
            abs_next_page_url = response.urljoin(next_page_url)
            yield Request(url = abs_next_page_url)



    def parse_page(self, response):
        #collect data only if isbn is available
        if(response.xpath('//*[@class="infoBoxRowTitle"]/text()').extract()[1].strip() == 'ISBN'):
            title = response.xpath('//h1[@id="bookTitle"]/text()').extract_first().strip()
            isbn = response.xpath('//*[@class="infoBoxRowItem"]/text()').extract()[1].strip()    #deleting the before and after trailing spaces

            lang = response.xpath('//*[@class="infoBoxRowItem"]/text()').extract()[3].strip()
            if(lang == ''):
                lang = "English"

            authorName = response.xpath('//*[@class="bookAuthorProfile__name"]/text()').extract_first().strip()
            aboutAuthor = response.xpath('//*[@class="bookAuthorProfile__about"]/span[2]/text()').extract()
            if aboutAuthor:
                aboutAuthor = "".join(aboutAuthor)
            else:
                aboutAuthor = "".join(response.xpath('//*[@class="bookAuthorProfile__about"]/span[1]/text()').extract())
            aboutAuthor = aboutAuthor.replace('See also: ', '')

            bookCount = random.randrange(200, 400)

            genres = ''
            gen = response.xpath('//*[@class="actionLinkLite bookPageGenreLink"][1]/text()').extract()
            gen_list = []
            for g in gen:
                if g not in gen_list:
                    gen_list.append(g)
            genres = ", ".join(gen_list)

            dscrp = response.xpath('//*[@id="description"]/span[2]/text()').extract()
            if len(dscrp) == 0:
                dscrp = response.xpath('//*[@id="description"]/span[1]/text()').extract()
            description = "\n\n".join(dscrp)

            bookRating = float(response.xpath('//*[@class="value rating"]/span/text()').extract_first())

            coverImage = response.xpath('//*[@id="coverImage"]/@src').extract_first()

            bookFormat = response.xpath('//*[@itemprop="bookFormat"]/text()').extract_first()
            numberOfPages = int(response.xpath('//*[@itemprop="numberOfPages"]/text()').extract_first().split()[0])

            if(bookFormat == "Hardcover"):
                cost = round(random.uniform(4, 6), 2)
            elif(bookFormat == "Paperback"):
                cost = round(random.uniform(2, 4), 2)
            else:
                cost = round(random.uniform(2, 5), 2)
            bookPrice = round((cost * 65.08), 2)

            info = response.xpath('//*[@id="details"]/div[2]/text()').extract_first().split()
            publishedYear = ''
            publisher = ''
            index = list(i for i,x in enumerate(info) if x == 'by')
            if index:
                publishedYear = generateYear(info, index)
                publisher = " ".join(info[index[0]+1:])

            voteCount = 0

            yield{
                'ISBN': isbn,
                'Title': title,
                'AuthorName' : authorName,
                'AboutAuthor' : aboutAuthor,
                'BookCount' : bookCount,
                'Genres' : genres,
                'Description' : description,
                'Lang': lang,
                'BookRating' : bookRating,
                'BookPrice' : bookPrice,
                'CoverImage' : coverImage,
                'BookFormat' : bookFormat,
                'NumberOfPages' : numberOfPages,
                'PublishedYear' : publishedYear,
                'Publisher' : publisher,
                'VoteCount' : voteCount
            }
