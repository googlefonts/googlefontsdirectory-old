package com.google.lint;

import com.google.inject.AbstractModule;
import com.google.inject.Singleton;
import com.google.inject.multibindings.Multibinder;
import com.google.lint.check.CheckCanonicalStyleNames;
import com.google.lint.check.CheckCanonicalWeights;
import com.google.lint.check.CheckFamilyNameMatchesFontNames;
import com.google.lint.check.CheckMetadataMatchesNameTable;
import com.google.lint.check.CheckNbspWidthMatchesSpWidth;
import com.google.lint.common.Context;
import com.google.lint.common.FontStore;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class LintModule extends AbstractModule {

  @Override
  protected void configure() {
    bind(MetadataStore.class).in(Singleton.class);
    bind(FontStore.class).in(Singleton.class);
    bind(Context.class).in(Singleton.class);

    Multibinder<LintCheck> multibinder = Multibinder.newSetBinder(binder(), LintCheck.class);
    multibinder.addBinding().to(CheckMetadataMatchesNameTable.class).in(Singleton.class);
    multibinder.addBinding().to(CheckFamilyNameMatchesFontNames.class).in(Singleton.class);
    multibinder.addBinding().to(CheckNbspWidthMatchesSpWidth.class).in(Singleton.class);
    multibinder.addBinding().to(CheckCanonicalStyleNames.class).in(Singleton.class);
    multibinder.addBinding().to(CheckCanonicalWeights.class).in(Singleton.class);
  }
}
