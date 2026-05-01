import settings
import bs4
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import WebBaseLoader


 # ----- METHOD 1 > 
loader = TextLoader('appolo.txt')
text_documents = loader.load()
print(text_documents)


#------- METHOD 2 > 
# Medium renders content for Googlebot (SEO purposes)
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

url1 = "https://medium.com/@aysebilgegunduz/everything-you-need-to-know-about-idor-insecure-direct-object-references-375f83e03a87"
url2 = "https://medium.com/@ud4y25/idor-vulnerabilities-explained-a-researchers-guide-to-authorization-flaws-82030def0e28"

bs_config = {
    "parse_only": bs4.SoupStrainer(
        class_=["pw-post-body-paragraph", "pw-post-title"]
    )
}

loader = WebBaseLoader(
    web_path=(url1, url2),
    bs_kwargs=bs_config,
    requests_kwargs={"headers": headers}
)

docs = loader.load()
print(docs)

