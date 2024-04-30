// eslint-disable-next-line @typescript-eslint/triple-slash-reference
/// <reference path="../support/index.d.ts" />

// These tests run through the chat flow.
describe('Settings', () => {
	// Wait for 2 seconds after all tests to fix an issue with Cypress's video recording missing the last few frames
	after(() => {
		// eslint-disable-next-line cypress/no-unnecessary-waiting
		cy.wait(2000);
	});

	beforeEach(() => {
		// Login as the admin user
		cy.loginAdmin();
		// Visit the home page
		cy.visit('/');
	});

	context('Ollama', () => {
		it('user can select a model', () => {
			// Click on the model selector
			cy.get('button[aria-label="Select a model"]').click();
			// Select the first model
			cy.get('div[role="option"][data-value]').first().click();
		});

		it('user can perform text chat', () => {
			// Click on the model selector
			cy.get('button[aria-label="Select a model"]').click();
			// Select the first model
			cy.get('div[role="option"][data-value]').first().click();
			// Type a message
			cy.get('#chat-textarea').type('Hi, what can you do? A single sentence only please.', {
				force: true
			});
			// Send the message
			cy.get('button[type="submit"]').click();
			// User's message should be visible
			cy.get('.chat-user').should('exist');
			// Wait for the response
			cy.get('.chat-assistant', { timeout: 120_000 }) // .chat-assistant is created after the first token is received
				.find('div[aria-label="Generation Info"]', { timeout: 120_000 }) // Generation Info is created after the stop token is received
				.should('exist');
		});
	});
});
