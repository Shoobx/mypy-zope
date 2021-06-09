import zope.interface


class Host:
    class IBookmark(zope.interface.Interface):
        def get_url() -> str:
            pass

    @zope.interface.implementer(IBookmark)
    class Bookmark:
        def get_url(self) -> str:
            return "http://"


bm: Host.IBookmark = Host.Bookmark()
reveal_type(bm)

"""
<output>
nested_definitions.py:16: note: Revealed type is "__main__.Host.IBookmark"
</output>
"""
