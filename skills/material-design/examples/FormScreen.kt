// FormScreen.kt
//
// Purpose: a sign-up form: labelled outlined text fields with supporting and error text, the
// right keyboard for each field, a secure password field, keyboard-safe scrolling, and one
// primary action.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x; foundation 1.13. Also valid on
//   material3 1.4.x (the TextFieldState overloads and OutlinedSecureTextField were added in
//   1.4.0). The value/onValueChange overloads still compile on 1.5 but are deprecated in
//   1.6.0-alpha01, so new code uses TextFieldState.
// Opt-ins: none.
// Resources assumed: R.string.create_account, back, name_label, name_error, email_label,
//   email_helper, email_error, password_label, password_helper, password_error;
//   R.drawable.ic_arrow_back. Manifest: android:windowSoftInputMode="adjustResize".
//
// Pages applied:
//   https://m3.material.io/components/text-fields/guidelines
//   https://m3.material.io/components/buttons/overview
//   https://developer.android.com/develop/ui/compose/text/user-input
//   https://developer.android.com/develop/ui/compose/system/insets-ui
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import android.util.Patterns
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.input.KeyboardActionHandler
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedSecureTextField
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp

data class NewAccount(val name: String, val email: String, val password: String)

@Composable
fun CreateAccountScreen(onSubmit: (NewAccount) -> Unit, onBack: () -> Unit) {
    // rememberTextFieldState is saveable: typed text survives rotation.
    val name = rememberTextFieldState()
    val email = rememberTextFieldState()
    val password = rememberTextFieldState()
    // Validate on submit, not on every keystroke: nobody is told "invalid" while still typing.
    var submitted by rememberSaveable { mutableStateOf(false) }

    val nameError = submitted && name.text.isBlank()
    val emailError = submitted && !Patterns.EMAIL_ADDRESS.matcher(email.text).matches()
    val passwordError = submitted && password.text.length < 8

    fun submit() {
        submitted = true
        val valid = name.text.isNotBlank() && password.text.length >= 8 &&
            Patterns.EMAIL_ADDRESS.matcher(email.text).matches()
        if (valid) onSubmit(NewAccount(name.text.toString(), email.text.toString(), password.text.toString()))
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.create_account)) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(painterResource(R.drawable.ic_arrow_back), contentDescription = stringResource(R.string.back))
                    }
                },
            )
        },
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .consumeWindowInsets(innerPadding) // so imePadding does not add the nav bar twice
                .imePadding()                      // keep fields and the button above the keyboard
                .verticalScroll(rememberScrollState()) // long forms and large font sizes must scroll
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            OutlinedTextField(
                state = name,
                modifier = Modifier.fillMaxWidth(),
                // A persistent label, never a placeholder as the only label: it stays visible
                // after typing and is what TalkBack announces.
                label = { Text(stringResource(R.string.name_label)) },
                // Error = isError (error colors) plus text that says how to fix it; never color alone.
                isError = nameError,
                supportingText = { if (nameError) Text(stringResource(R.string.name_error)) },
                lineLimits = TextFieldLineLimits.SingleLine,
                // The action key moves to the next field.
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words, imeAction = ImeAction.Next),
            )
            OutlinedTextField(
                state = email,
                modifier = Modifier.fillMaxWidth(),
                label = { Text(stringResource(R.string.email_label)) },
                isError = emailError,
                // Helper text gives the expected format up front; the error text replaces it.
                supportingText = {
                    Text(stringResource(if (emailError) R.string.email_error else R.string.email_helper))
                },
                lineLimits = TextFieldLineLimits.SingleLine,
                // Email keyboard (with @), no autocorrect.
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Email, autoCorrectEnabled = false, imeAction = ImeAction.Next,
                ),
            )
            // A dedicated secure field that obfuscates what is typed (material3 1.4+).
            OutlinedSecureTextField(
                state = password,
                modifier = Modifier.fillMaxWidth(),
                label = { Text(stringResource(R.string.password_label)) },
                isError = passwordError,
                supportingText = {
                    Text(stringResource(if (passwordError) R.string.password_error else R.string.password_helper))
                },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password, imeAction = ImeAction.Done),
                // Done on the last field submits, the same as the button.
                onKeyboardAction = KeyboardActionHandler { submit() },
            )
            // One filled button: the single highest-emphasis action on the screen. It stays
            // enabled so that tapping it can explain what is missing; a disabled button cannot.
            Button(onClick = { submit() }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                Text(stringResource(R.string.create_account))
            }
        }
    }
}
