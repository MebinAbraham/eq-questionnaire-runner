local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  title: title,
  id: 'school-travel-question',
  description: description,
  type: 'General',
  answers: [
    {
      id: 'school-travel-answer',
      mandatory: false,
      options: [
        {
          label: 'Driving a car or van',
          value: 'Driving a car or van',
        },
        {
          label: 'Passenger in a car or van',
          value: 'Passenger in a car or van',
        },
        {
          label: 'Car or van pool, sharing driving',
          value: 'Car or van pool, sharing driving',
        },
        {
          label: 'Bus, minibus or coach (public or private)',
          value: 'Bus, minibus or coach (public or private)',
        },
        {
          label: 'On foot',
          value: 'On foot',
        },
        {
          label: 'Taxi',
          value: 'Taxi',
        },
        {
          label: 'Train',
          value: 'Train',
        },
        {
          label: 'Bicycle',
          value: 'Bicycle',
        },
        {
          label: 'Motorcycle, scooter or moped',
          value: 'Motorcycle, scooter or moped',
        },
        {
          label: 'Other',
          value: 'Other',
        },
      ],
      type: 'Radio',
    },
  ],
};


local nonProxyTitleSchool = 'How do you usually travel to your place of study, including school?';
local proxyTitleSchool = {
  text: 'How does <em>{person_name}</em> usually travel to their place of study, including school?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDescriptionSchool = 'Select one option only, for the longest part, by distance, of your usual journey to place of study.';
local proxyDescriptionSchool = 'Select one option only, for the longest part, by distance, of thier usual journey to place of study.';

{
  type: 'Question',
  id: 'school-travel',
  question_variants: [
    {
      question: question(nonProxyTitleSchool, nonProxyDescriptionSchool),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitleSchool, proxyDescriptionSchool),
      when: [rules.proxyYes],
    },
  ],
}