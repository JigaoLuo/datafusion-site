from pelican import signals
from pelican.contents import Tag

def process_tags_in_generator(generator):
    """
    Find tags that look like '[tag1, tag2]' and split them into individual tags.
    This function manipulates the generator's internal state.
    """
    
    tag_objects_by_name = {tag.name: tag for tag in generator.tags}
    tags_to_remove = []

    for tag, articles in list(generator.tags.items()):
        if '[' in tag.name:
            tags_to_remove.append(tag)

            for article in articles:
                article.tags = [t for t in article.tags if t.name != tag.name]

                cleaned_names = tag.name.replace('[', '').replace(']', '').split(',')

                for name in cleaned_names:
                    name = name.strip()
                    if not name:
                        continue

                    if name in tag_objects_by_name:
                        new_tag = tag_objects_by_name[name]
                    else:
                        new_tag = Tag(name, generator.settings)
                        tag_objects_by_name[name] = new_tag

                    if new_tag not in article.tags:
                        article.tags.append(new_tag)

                    if new_tag not in generator.tags:
                        generator.tags[new_tag] = []
                    if article not in generator.tags[new_tag]:
                        generator.tags[new_tag].append(article)

    for tag in tags_to_remove:
        if tag in generator.tags:
            del generator.tags[tag]

def register():
    signals.article_generator_finalized.connect(process_tags_in_generator)