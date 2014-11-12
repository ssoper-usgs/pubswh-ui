'''
Created on Nov 10, 2014

@author: ayan
'''


def get_publication_type(json_content):
    """
    Parse JSON content to get the publication
    type for display with recent publications.
    
    :param dict json_content: JSON data as a Python dictionary
    :return: publication type, possibly with page number
    :rtype: str 
    """
    try:
        pub_type = json_content['largerWorkSubtype']['text'] # try to get the publication type from largerWorkSubtype
    except KeyError:
        pub_type = json_content['publicationSubtype']['text'] # failing that, try to get it from publicationSubtype
    except KeyError:
        pub_type = json_content['seriesTitle']['text'] # failing that, try to get it from the seriesTitle
    if pub_type != 'Journal Article':
        pub_year = json_content['publicationYear']
        display_pub_type = '{publication_type}: {publication_year}'.format(publication_type=pub_type, publication_year=pub_year)
    else:
        display_pub_type = pub_type
    return display_pub_type


def display_publication_info(json_content):
    publication_year = json_content['publicationYear']
    series_title_text = json_content['seriesTitle']['text']
    if json_content.get('seriesTitle', None) and json_content.get('seriesNumber', None):
        series_number = json_content['seriesNumber']
        chapter = json_content.get('chapter', None)
        subchapter = json_content.get('subChapter', None)
        if chapter and subchapter:
            pub_info = '{publication_year}, {title} {series_number} {chapter} {subchapter}'.format(publication_year=publication_year,
                                                                                                   title=series_title_text,
                                                                                                   series_number=series_number,
                                                                                                   chapter=chapter,
                                                                                                   subchapter=subchapter
                                                                                                   )
        elif chapter and not subchapter:
            pub_info = '{publication_year}, {title} {series_number} {chapter}'.format(publication_year=publication_year,
                                                                                      title=series_title_text,
                                                                                      series_number=series_number,
                                                                                      chapter=chapter
                                                                                      )
        else:
            pub_info = '{publication_year}, {title} {series_number}'.format(publication_year=publication_year,
                                                                            title=series_title_text,
                                                                            series_number=series_number
                                                                            )
        full_pub_info = pub_info           
    elif json_content.get('seriesTitle', None) and json_content.get('publicationType', None).get('text', None) == 'Article':
        start_page = json_content.get('startPage', None)
        end_page = json_content.get('endPage', None)
        try:
            volume = json_content['volume']
            pub_info = '{publication_year}, {title} ({volume}) {start_page}'.format(publication_year=publication_year,
                                                                                    title=series_title_text,
                                                                                    volume=volume,
                                                                                    start_page=start_page
                                                                                    )
        except KeyError:
            volume = None
            pub_info = '{publication_year}, {title} {start_page}'.format(publication_year=publication_year,
                                                                         title=series_title_text
                                                                         )
        if end_page:
            full_pub_info = '{pub_info}-{end_page}'.format(pub_info=pub_info, end_page=end_page)
        else:
            full_pub_info = pub_info
    else:
        pass
    return full_pub_info
        