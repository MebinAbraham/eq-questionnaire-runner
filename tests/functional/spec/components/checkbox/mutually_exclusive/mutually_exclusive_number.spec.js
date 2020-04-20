const NumberPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page');

const SectionSummaryPage = require('../../../../base_pages/section-summary.page.js');

describe('Component: Mutually Exclusive Number With Single Checkbox Override', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_mutually_exclusive.json');
    browser.url('/questionnaire/mutually-exclusive-number');
  });

  describe('Given the user has entered a value for the non-exclusive number answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      // Given
      $(NumberPage.number()).setValue('123');
      expect($(NumberPage.number()).getValue()).to.contain('123');

      // When
      $(NumberPage.numberExclusiveIPreferNotToSay()).click();

      // Then
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(NumberPage.number()).getValue()).to.contain('');

      $(NumberPage.submit()).click();

      expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.have.string('I prefer not to say');
      expect($(SectionSummaryPage.summaryItems()).getText()).to.not.have.string('123');
    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.', function() {
      // Given
      $(NumberPage.numberExclusiveIPreferNotToSay()).click();
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(NumberPage.number()).setValue('123');

      // Then
      expect($(NumberPage.number()).getValue()).to.contain('123');
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(NumberPage.submit()).click();

      expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.have.string('123');
      expect($(SectionSummaryPage.summaryItems()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.', function() {
      // Given
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(NumberPage.number()).setValue('123');

      // Then
      expect($(NumberPage.number()).getValue()).to.contain('123');
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(NumberPage.submit()).click();

      expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.have.string('123');
      expect($(SectionSummaryPage.summaryItems()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not answered the non-exclusive number answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      // Given
      expect($(NumberPage.number()).getValue()).to.contain('');

      // When
      $(NumberPage.numberExclusiveIPreferNotToSay()).click();
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      $(NumberPage.submit()).click();

      expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.have.string('I prefer not to say');
      expect($(SectionSummaryPage.summaryItems()).getText()).to.not.have.string('123');
    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      // Given
      expect($(NumberPage.number()).getValue()).to.contain('');
      expect($(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(NumberPage.submit()).click();

      // Then
      expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.contain('No answer provided');
    });
  });
});
