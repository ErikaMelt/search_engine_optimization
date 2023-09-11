import json
import os
import sys

from gpt_model.gpt_35_model import generate_evaluation

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)

from database.models.create_tables import setup_database
from database.repository.search_results_repository import add
from database.repository.query_intent_repository import get_queries
from scraper.scraper import scrape_bing


script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)


if __name__ == "__main__":

    data = {
        "intents": [
            {
                "intent": "I'm trying to figure out the most effective way to make paper tape stick to a wound wrapped in gauze.",
                "results": [
                    {
                        "title": "How to Make a Bandage: The Definitive Guide to …",
                        "snippet": "https://www.primalsurvivor.net/how-to-make-bandageStep 1: Stop the Bleeding Before you worry about bandaging the wound, you need stop the bleeding. Elevate the wound above the heart and apply pressure. Ideally you would apply pressure with a clean compress, such as a heavy gauze pad. However, at this stage, stopping the bleeding is more important … Ver másStep 1: Stop The BleedingBefore you worry about bandaging the wound, you need stop the bleeding. Elevate the wound above the heart and apply pressure. Ideally … Ver másStep 2: Prepare The WoundBefore applying the bandage, you’ll need to: 1. Wash your hands. 2. Clean the wound. 3. Apply antiseptic ointment or Vaseline to the wound. This aids healing, keeps the wound … Ver másStep 4: Apply The BandageThe bandage is what holds the wound in place. Bandages also can apply pressure to the wound to help control bleeding. Because the bandage … Ver másStep 3: Apply A Wound DressingBandages are made out of two parts: a dressing and the bandage. The dressing goes directly against the wound and the bandage is what holds … Ver másDe primalsurvivor.netContenidoStep 1: Stop The BleedingStep 2: Prepare The WoundStep 3: Apply A Wound DressingStep 4: Apply The BandageVer todas las secciones",
                        "url": "https://www.primalsurvivor.net/how-to-make-bandage/",
                    },
                    {
                        "title": "Healthfullyhttps://healthfully.com/homemade-bandages",
                        "snippet": "Web27 de jul. de 2017 · Making an Emergency Bandage. Find some gauze to use as a dressing for the wound. If gauze is not available, use a paper towel. Find some sticky tape. Any kind will do. It will be used to hold the dressing in place. Cut or tear the gauze or paper towel into the right shape and size for the wound you are dressing.",
                        "url": "https://healthfully.com/homemade-bandages-7397300.html",
                    },
                ],
            },
            {
                "intent": "I want to find out more details of the murder case against Zachary Latham.",
                "results": [
                    {
                        "title": "nytimes.comhttps://www.nytimes.com/2020/08/07/nyregion/tiktok-manslaughter-new...",
                        "snippet": "Web7 de ago. de 2020 · 70 Zachary Latham, 18, is charged with manslaughter in the killing of William Durham in South Jersey. Cumberland County, N.J., Department of Corrections By Ed Shanahan Aug. 7, 2020 Zachary...",
                        "url": "https://www.nytimes.com/2020/08/07/nyregion/tiktok-manslaughter-new-jersey.html",
                    },
                    {
                        "title": "showbizcast.comhttps://showbizcast.com/where-is-zachary-latham-now",
                        "snippet": "Web1 de jun. de 2022 · As we said earlier, Zachary Latham is a TikTok user who killed his neighbor and captured the incident to get famous. He stabbed veteran corrections officer named William Durham Sr. on May 4, 2020. It happened after an argument that started near the victim's house and ended in Latham's garage. [image-2]",
                        "url": "https://showbizcast.com/where-is-zachary-latham-now",
                    },
                ],
            },
        ]
    }

    json_data = json.dumps(data)

    evaluation = generate_evaluation(json_data)
    print(evaluation)

    #setup_database()
    #queries_data = get_queries(20)

    #if queries_data:
        #for query, query_id in queries_data:
            #print(query.query, query_id)
            #search_results = scrape_bing(query.query, query_id)
            #if search_results:
                #add(search_results)
