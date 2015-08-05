"""
...
"""
class CourseStructureTransformation(object):
    """
    ...
    """

    # TODO 8874: Add versioning system to transformations (MA-1121)

    @property
    def id(self):
        """
        Returns:
            str
        """
        return self.__class__.__name__

    @property
    def required_fields(self):
        """
        Specifies XBlock fields that are required by this transformation's
        apply method.

        Returns:
            set[str]
        """
        return set()

    def collect(self, course_key, block_structure, xblock_dict):
        """
        Computes any information for each XBlock that's necessary to execute
        this transformation's apply method.

        Arguments:
            course_key (CourseKey)
            block_structure (CourseBlockStructure)
            xblock_dict (dict[UsageKey: XBlock])

        Returns:
            dict[UsageKey: dict]
        """
        # TODO 8874: Instead of returning a dict of dicts, encapsulate data collection in a nice DataCollector class or something.
        return None

    def apply(self, user, course_key, block_structure, block_data, remove_orphans):
        """
        Mutates block_structure and block_data based on the given user_info.

        Arguments:
            user (UserCourseInfo)
            course_key (CourseKey)
            block_structure (CourseBlockStructure)
            block_data (dict[UsageKey: CourseBlockData])
            remove_orphans (bool)
        """
        pass
