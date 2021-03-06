from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListChangeEvaluatesSections(IntegrationTestCase):
    def add_person(self, first_name, last_name):
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": first_name, "last-name": last_name})

    def get_link(self, rowIndex, text):
        selector = f"tbody:nth-child({rowIndex}) td:last-child a"
        selected = self.getHtmlSoup().select(selector)

        filtered = [html for html in selected if text in html.get_text()]

        return filtered[0].get("href")

    def get_previous_link(self):
        selector = "#top-previous"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def test_wihout_primary_person(self):
        self.launchSurvey("test_list_change_evaluates_sections")

        self.get("/questionnaire/sections/who-lives-here/")
        self.assertEqualUrl("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "No"})
        self.assertEqualUrl("/questionnaire/list-collector/")

        self.post({"anyone-else": "No"})
        self.assertEqualUrl("/questionnaire/")

        self.get("/questionnaire/sections/accommodation-section/")
        self.assertEqualUrl("/questionnaire/accommodation-type/")

        self.post()
        self.post()
        self.post()
        self.assertEqualUrl("/questionnaire/")

        self.get("/questionnaire/sections/who-lives-here/")
        self.assertEqualUrl("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "No"})

        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.assertEqualUrl("/questionnaire/")

        self.assertInSelector(
            "Partially completed", "tbody:nth-child(2) td:nth-child(2)"
        )

        self.get("questionnaire/sections/accommodation-section/")
        self.assertEqualUrl("/questionnaire/own-or-rent/?resume=True")

    def test_with_primary_person(self):
        self.launchSurvey("test_list_change_evaluates_sections")

        self.get("/questionnaire/sections/accommodation-section/")
        self.post()
        self.post()
        self.assertEqualUrl("/questionnaire/sections/accommodation-section/")
        self.post()

        self.assertInSelector("Completed", "tbody:nth-child(2) td:nth-child(2)")

        self.get("/questionnaire/sections/who-lives-here/")
        self.assertEqualUrl("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})

        self.assertEqualUrl("/questionnaire/")
        self.assertInSelector(
            "Partially completed", "tbody:nth-child(2) td:nth-child(2)"
        )
